#!/usr/bin/env python3
"""Resolve public Amazon redirects without downloading Amazon product pages."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse, urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen
from urllib.error import HTTPError

SHORT = {'amzn.eu', 'amzn.to', 'a.co'}
MARKETPLACES = {'de': ('amazon.de', 3), 'com': ('amazon.com', 1),
                'co.uk': ('amazon.co.uk', 2), 'fr': ('amazon.fr', 4),
                'it': ('amazon.it', 8), 'es': ('amazon.es', 9),
                'nl': ('amazon.nl', 14), 'se': ('amazon.se', 15),
                'pl': ('amazon.pl', 16), 'co.jp': ('amazon.co.jp', 5),
                'ca': ('amazon.ca', 6)}
ASIN_PATH = re.compile(r'/(?:dp|gp/product|gp/aw/d|product)/([A-Z0-9]{10})(?:[/?]|$)', re.I)


class Resolved(Exception):
    def __init__(self, url):
        self.url = url


def marketplace(host):
    host = host.lower().removeprefix('www.')
    for key, (name, _) in MARKETPLACES.items():
        if host == name or host.endswith('.' + name):
            return key
    return None


def _capture_redirect(short_url):
    class StopBeforeAmazon(HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            parsed = urlparse(newurl)
            if parsed.scheme != 'https' or not parsed.hostname:
                raise ValueError('Redirect to non-HTTPS or invalid host')
            host = parsed.hostname.lower()
            if marketplace(host):
                raise Resolved(newurl)  # HTTP redirect headers, never Amazon HTML
            if host not in SHORT:
                raise ValueError('Redirect to an unexpected host')
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    opener = build_opener(StopBeforeAmazon())
    for method in ('HEAD', 'GET'):
        try:
            with opener.open(Request(short_url, method=method), timeout=9) as response:
                # A shortener may return a URL without any redirect.
                if marketplace(urlparse(response.geturl()).hostname or ''):
                    return response.geturl()
        except Resolved as exc:
            return exc.url
        except HTTPError as exc:
            if exc.code not in (403, 405, 501) or method == 'GET':
                raise ValueError('Amazon short link could not be resolved') from exc
        except (TimeoutError, OSError) as exc:
            if method == 'GET':
                raise ValueError('Amazon short link could not be resolved') from exc
    raise ValueError('Short URL did not redirect to a supported Amazon site')


def resolve(raw, default_marketplace='de'):
    raw = raw.strip()
    if default_marketplace not in MARKETPLACES:
        raise ValueError('Unsupported marketplace')
    if re.fullmatch(r'[A-Z0-9]{10}', raw, re.I):
        asin, code, source = raw.upper(), default_marketplace, 'asin'
    else:
        url = urlparse(raw)
        host = (url.hostname or '').lower()
        if url.scheme != 'https' or url.username or url.password:
            raise ValueError('Supply an HTTPS Amazon product or short link')
        if host in SHORT:
            raw = _capture_redirect(raw)
            url = urlparse(raw)
            source = 'short-link-redirect'
        else:
            source = 'product-url'
        code = marketplace(url.hostname or '')
        if code is None:
            raise ValueError('Not a supported Amazon marketplace')
        match = ASIN_PATH.search(url.path)
        if match:
            asin = match.group(1).upper()
        else:
            possible = parse_qs(url.query).get('asin') or parse_qs(url.query).get('ASIN')
            if not possible or not re.fullmatch(r'[A-Z0-9]{10}', possible[0], re.I):
                raise ValueError('ASIN not found in redirect URL; no product-page scraping attempted')
            asin = possible[0].upper()
    site, keepa_id = MARKETPLACES[code]
    chart = 'https://graph.keepa.com/pricehistory.png?' + urlencode(
        {'asin': asin, 'domain': code, 'amazon': 1, 'new': 1, 'used': 1, 'range': 365})
    return {'asin': asin, 'marketplace': code, 'source_type': source,
            'amazon_url': f'https://www.{site}/dp/{asin}',
            'keepa_url': f'https://keepa.com/#!product/{keepa_id}-{asin}',
            'chart_candidate': chart,
            'chart_status': 'unverified unofficial legacy URL; inspect for valid data'}


def download_chart(url, filename):
    # Caller can request a chart; this does NOT use the paid Keepa API.
    if urlparse(url).hostname != 'graph.keepa.com':
        raise ValueError('Chart hostname is not Keepa')
    with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=12) as response:
        content = response.read(5 * 1024 * 1024 + 1)
    if len(content) > 5 * 1024 * 1024 or not content.startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError('No valid small PNG chart returned')
    Path(filename).write_bytes(content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url', help='Amazon ASIN or full/short HTTPS URL')
    parser.add_argument('--marketplace', choices=sorted(MARKETPLACES), default='de')
    parser.add_argument('--download-chart', metavar='PNG_PATH')
    args = parser.parse_args()
    try:
        record = resolve(args.url, args.marketplace)
        if args.download_chart:
            download_chart(record['chart_candidate'], args.download_chart)
            record['chart_file'] = args.download_chart
            record['chart_status'] = 'downloaded; visually inspect whether it contains valid price traces'
        print(json.dumps(record, indent=2))
    except (OSError, ValueError) as exc:
        parser.exit(status=2, message=f'Error: {exc}\n')


if __name__ == '__main__':
    main()
