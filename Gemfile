source "https://rubygems.org"

# 使用 Jekyll 4.x，由 GitHub Actions 构建部署
# 不再依赖 github-pages gem，从而可以使用新版 Jekyll 和更多插件
gem "jekyll", "~> 4.3.4"
gem "minima", "~> 2.5"

# 保持 GitHub Flavored Markdown 解析行为一致
gem "kramdown-parser-gfm"

group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.17"
  gem "jekyll-seo-tag", "~> 2.8"
  gem "jekyll-sitemap", "~> 1.4"
end

# 测试/质量检查依赖（部署时通过 BUNDLE_WITHOUT=test 跳过）
group :test do
  gem "html-proofer", "~> 5.0", require: false
end

# Windows 不包含 zoneinfo 文件，所以需额外安装
gem "tzinfo-data", platforms: [:windows, :jruby]

# Windows 平台监听目录的依赖
gem "wdm", "~> 0.1.1" if Gem.win_platform?
