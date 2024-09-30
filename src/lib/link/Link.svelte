<script lang="ts">
    import type {HTMLAttributes} from "svelte/elements";
    import {cn} from "$lib/utils";
    import { page } from '$app/stores';

    type $$Props = HTMLAttributes<HTMLDivElement>;

    let className: $$Props["class"] = undefined;
    export { className as class };

    export let href: string = '#'
    $: isActive = $page.url.pathname.startsWith(href)

</script>


<a
        class={cn("font-medium cursor-pointer text-muted-foreground transition-colors hover:text-foreground", className, isActive ? 'text-foreground font-bold' : '')} {...$$restProps}
        href="{href}"
>
    <slot/>
</a>
