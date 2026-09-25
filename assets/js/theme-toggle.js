/*!
 * 主题切换：自动（跟随系统）→ 亮色 → 暗色 → 自动
 *
 * - 状态保存在 localStorage.theme
 * - 亮/暗通过 <html data-theme="light|dark"> 覆盖 CSS；
 *   选择「自动」时移除该属性，交回 prefers-color-scheme
 * - 首次访问（无 localStorage）默认「自动」
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'theme';
  var MODES = ['auto', 'light', 'dark'];
  var LABELS = { auto: '跟随系统', light: '亮色', dark: '暗色' };
  var THEME_COLORS = { light: '#faf9f6', dark: '#1c1b19' };

  var root = document.documentElement;
  var button = document.getElementById('theme-toggle');
  var meta = document.querySelector('meta[name="theme-color"]');
  var buttonText = button && button.querySelector('.theme-toggle-text');
  var media = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

  if (!button) {
    return;
  }

  function currentMode() {
    try {
      var mode = localStorage.getItem(STORAGE_KEY);
      return MODES.indexOf(mode) > -1 ? mode : 'auto';
    } catch (e) {
      return 'auto';
    }
  }

  function apply(mode) {
    if (mode === 'auto') {
      root.removeAttribute('data-theme');
    } else {
      root.setAttribute('data-theme', mode);
    }

    if (buttonText) {
      buttonText.textContent = LABELS[mode];
    }
    button.setAttribute('aria-label', '切换主题，当前：' + LABELS[mode]);
    button.title = '主题：' + LABELS[mode] + '（点击切换）';

    if (meta) {
      var effective = mode === 'auto' ? (media && media.matches ? 'dark' : 'light') : mode;
      meta.setAttribute('content', THEME_COLORS[effective]);
    }
  }

  button.addEventListener('click', function () {
    var next = MODES[(MODES.indexOf(currentMode()) + 1) % MODES.length];
    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch (e) {}
    apply(next);
  });

  // 处于「自动」时，系统偏好变化需要同步 theme-color
  if (media) {
    var onSystemChange = function () {
      if (currentMode() === 'auto') {
        apply('auto');
      }
    };
    if (media.addEventListener) {
      media.addEventListener('change', onSystemChange);
    } else if (media.addListener) {
      media.addListener(onSystemChange);
    }
  }

  apply(currentMode());
})();
