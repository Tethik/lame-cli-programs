from requests_html import session
import requests
import click
import shutil


@click.group()
def cli():
    pass


@cli.command('list')
def list_versions():
    r = session.get('https://mcversions.net/')
    server_links = r.html.find('.server')
    versions = list(map(lambda s: f"* {s.attrs['download']}", server_links))
    print("\n".join(versions))


@cli.command('download')
@click.argument('version')
def download_version(version):
    r = session.get('https://mcversions.net/')
    server_links = r.html.find('.server')
    download_link = list(filter(lambda s: s.attrs['download'] == version, server_links))[0].attrs['href'] # type: str    
    click.echo(f"Downloading {version} from {download_link}")
    # Lazy security check
    assert download_link.startswith("https://launcher.mojang.com")
    with requests.get(download_link, stream=True) as r:
        with open(version, 'wb') as f:        
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def main():
    cli()

if __name__ == "__main__":
    cli()
