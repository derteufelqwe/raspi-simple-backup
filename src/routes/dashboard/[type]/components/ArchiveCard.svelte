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
    import * as Table from "$lib/components/ui/table";
    import * as Collapsible from "$lib/components/ui/collapsible/index.js";
    import { Skeleton } from "$lib/components/ui/skeleton";
    import { Badge } from "$lib/components/ui/badge";
    import {ChevronDown, DockIcon, FolderArchiveIcon} from "lucide-svelte";
    import type {BackupArchive} from "../../../types";

    export let data: BackupArchive;

    // --- Functions ---

    function formatDate(dateString: string) {
        return dateString.split('T')[0].split('-').toReversed().join('.')
    }

    function getAgeInDays(dateString: string) {
        let ageMs = new Date().getTime() - new Date(dateString).getTime();

        return Math.floor(ageMs / (1000 * 3600 * 24));  // ms -> days
    }

</script>


<Card>
    <Collapsible.Root>
        <CardHeader>
            <div class="flex flex-row gap-4">
                <div>
                    <FolderArchiveIcon class="text-muted-foreground h-7 w-7"/>
                </div>
                <div>
                    <CardTitle>Backup from {formatDate(data.timestamp)}</CardTitle>
                    <CardDescription>{data.filename}</CardDescription>
                </div>
                <div>
                    <Badge variant="outline" class="border-amber-500 bg-amber-200">{getAgeInDays(data.timestamp)} days ago</Badge>
                </div>
                <div>
                    <Badge variant="outline" class="border-blue-500 bg-blue-200">123 MB</Badge>
                </div>
                <div class="ml-auto">
                    <Collapsible.Trigger asChild let:builder>
                        <Button builders={[builder]} variant="ghost" size="sm" class="w-9 p-0 border-2">
                            <ChevronDown class="h-5 w-5"/>
                            <span class="sr-only">Toggle</span>
                        </Button>
                    </Collapsible.Trigger>
                </div>
            </div>
        </CardHeader>

        <Collapsible.Content>
            <CardContent>
                <Table.Root>
<!--                    <Table.Caption>Backed Folders</Table.Caption>-->
                    <Table.Header>
                        <Table.Row>
                            <Table.Head>Filename</Table.Head>
                            <Table.Head>Checksum</Table.Head>
                            <Table.Head>Size</Table.Head>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {#each data.checksums as checksum}
                            <Table.Row>
                                <Table.Cell class="font-medium">{checksum.file}</Table.Cell>
                                <Table.Cell class="font-mono">{checksum.checksum}</Table.Cell>
                                <Table.Cell>???</Table.Cell>
                            </Table.Row>
                        {/each}
                    </Table.Body>
                </Table.Root>
            </CardContent>
        </Collapsible.Content>
    </Collapsible.Root>
</Card>
