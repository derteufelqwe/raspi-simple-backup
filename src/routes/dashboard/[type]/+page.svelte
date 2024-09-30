<script lang="ts">
    import {Button} from "$lib/components/ui/button"
    import {
        Card,
        CardContent,
        CardDescription,
        CardFooter,
        CardHeader,
        CardTitle,
    } from "$lib/components/ui/card"
    import {Checkbox} from "$lib/components/ui/checkbox"
    import {Input} from "$lib/components/ui/input"
    import {Link} from "$lib/link";
    import {page} from '$app/stores';
    import type {RequestData} from "./types";
    import ArchiveCard from "./components/ArchiveCard.svelte";
    import {onMount} from "svelte";
    import ArchiveCardLoading from "./components/ArchiveCardLoading.svelte";

    let loading = true;
    let data: RequestData
    $: type = $page.params.type satisfies string
    $: loadData(type)

    // --- Functions ---

    async function loadData(type: string) {
        loading = true;
        if (!["daily", "weekly", "monthly", "yearly"].includes(type)) {
            throw new Error("Invalid type value");
        }

        const request = await fetch('/api/files/' + type);
        const response = await request.json();

        loading = false;
        data = response;
    }

    function capitalize(text: string) {
        return text.charAt(0).toUpperCase() + text.toLowerCase().slice(1);
    }

</script>


<div class="mx-auto grid w-full max-w-6xl gap-2">
    <h1 class="text-3xl font-semibold">{capitalize(type)} Backups</h1>
</div>
<div class="mx-auto grid w-full max-w-6xl items-start gap-6 md:grid-cols-[180px_1fr] lg:grid-cols-[250px_1fr]">
    <nav class="grid gap-4 text-sm text-muted-foreground">
        <Link href="/dashboard/daily">Daily</Link>
        <Link href="/dashboard/weekly">Weekly</Link>
        <Link href="/dashboard/monthly">Monthly</Link>
        <Link href="/dashboard/yearly">Yearly</Link>
    </nav>

    <div class="grid gap-6">
        {#if !loading}
            {#if data.files.length === 0}
                No Files available
            {:else}
                {#each data.files as fileData}
                    <ArchiveCard data={fileData}/>
                {/each}
            {/if}
        {:else}
            {#each Array(7) as _}
                <ArchiveCardLoading/>
            {/each}
        {/if}
    </div>
</div>
