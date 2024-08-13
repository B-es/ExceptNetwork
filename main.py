from proxy_exception_adderer import ProxyExceptionAdderer
from tk_ui.build_page import start_app


if __name__ == '__main__':
    proxy_exception_adderer = ProxyExceptionAdderer()
    start_app(proxy_exception_adderer)
