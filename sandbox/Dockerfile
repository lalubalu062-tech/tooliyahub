FROM ubuntu:22.04

# Timezone aur basic setup
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    nodejs npm \
    php-cli \
    wget curl unzip xvfb \
    libnss3 libxss1 libasound2 fonts-liberation libappindicator3-1 xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome for Scraping
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Python Scraping Libraries (Playwright, Selenium, DrissionPage)
RUN pip3 install --no-cache-dir selenium playwright DrissionPage requests beautifulsoup4
RUN playwright install chromium
RUN playwright install-deps

WORKDIR /workspace
CMD ["tail", "-f", "/dev/null"]
