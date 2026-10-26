<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/state';
  import { Button } from '#lib/components/ui/button';
  import * as Empty from '#lib/components/ui/empty';
  import { readSavedLocale, saveLocale } from '#lib/locale';
  import type { Locale } from '#lib/types';

  let locale = $state<Locale>('zh');
  const t = (zh: string, en: string) => locale === 'zh' ? zh : en;
  const title = $derived(page.status === 404
    ? t('找不到这道题', 'Problem not found')
    : t('页面暂时无法打开', 'Unable to open this page'));

  onMount(() => { locale = readSavedLocale(); });
  $effect(() => { document.documentElement.lang = locale === 'zh' ? 'zh-CN' : 'en'; });

  function changeLocale() {
    locale = locale === 'zh' ? 'en' : 'zh';
    saveLocale(locale);
  }
</script>

<svelte:head>
  <title>{title} · Fieldnotes · ECSE 2100</title>
  <meta name="description" content={t('返回习题室继续学习。', 'Return to the study room to keep learning.')} />
</svelte:head>

<main class="error-page">
  <Empty.Root>
    <Empty.Header>
      <p>{page.status} · Fieldnotes</p>
      <Empty.Title><h1>{title}</h1></Empty.Title>
      <Empty.Description>{page.status === 404
        ? t('链接可能已失效，或这份试卷暂未收录。', 'The link may be outdated, or this paper may be unavailable.')
        : t('请稍后重试，或返回习题室选择其他题目。', 'Try again later, or return to the study room to choose another problem.')}</Empty.Description>
    </Empty.Header>
    <Empty.Content>
      <div class="flex flex-wrap justify-center gap-2">
        <Button href="/">{t('返回习题室', 'Back to study room')}</Button>
        <Button variant="outline" onclick={changeLocale} aria-label={t('Switch to English', '切换为中文')}>
          <span lang={locale === 'zh' ? 'en' : 'zh-CN'}>{locale === 'zh' ? 'EN' : '中文'}</span>
        </Button>
      </div>
    </Empty.Content>
  </Empty.Root>
</main>
