<script lang="ts">
  import { renderMath } from '#lib/math';
  let {tex, display = false, boxed = false}: {tex: string; display?: boolean; boxed?: boolean} = $props();
  const html = $derived(renderMath(boxed ? `\\boxed{${tex}}` : tex, display));
</script>
<span class:math-display={display} class:math-inline={!display} data-math={tex}>{@html html}</span>
