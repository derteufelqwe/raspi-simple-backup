<script lang="ts">
    import {CircleUser, Menu, Package2, Search} from "lucide-svelte"
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
    import {
        DropdownMenu,
        DropdownMenuContent,
        DropdownMenuItem,
        DropdownMenuLabel,
        DropdownMenuSeparator,
        DropdownMenuTrigger,
    } from "$lib/components/ui/dropdown-menu"
    import {Input} from "$lib/components/ui/input"
    import {Sheet, SheetContent, SheetTrigger} from "$lib/components/ui/sheet"
    import {Link} from "$lib/link";

</script>


<div class="mx-auto grid w-full max-w-6xl gap-2">
    <h1 class="text-3xl font-semibold">Settings</h1>
</div>
<div class="mx-auto grid w-full max-w-6xl items-start gap-6 md:grid-cols-[180px_1fr] lg:grid-cols-[250px_1fr]">
    <nav
            class="grid gap-4 text-sm text-muted-foreground" x-chunk="dashboard-04-chunk-0"
    >
        <Link href="#" class="font-semibold text-primary">
            General
        </Link>
        <Link href="#">Security</Link>
        <Link href="#">Integrations</Link>
        <Link href="#">Support</Link>
        <Link href="#">Organizations</Link>
        <Link href="#">Advanced</Link>
    </nav>
    <div class="grid gap-6">
        <Card x-chunk="dashboard-04-chunk-1">
            <CardHeader>
                <CardTitle>Store Name</CardTitle>
                <CardDescription>
                    Used to identify your store in the marketplace.
                </CardDescription>
            </CardHeader>
            <CardContent>
                <form>
                    <Input placeholder="Store Name" />
                </form>
            </CardContent>
            <CardFooter class="border-t px-6 py-4">
                <Button>Save</Button>
            </CardFooter>
        </Card>
        <Card x-chunk="dashboard-04-chunk-2">
            <CardHeader>
                <CardTitle>Plugins Directory</CardTitle>
                <CardDescription>
                    The directory within your project, in which your plugins are
                    located.
                </CardDescription>
            </CardHeader>
            <CardContent>
                <form class="flex flex-col gap-4">
                    <Input
                            placeholder="Project Name"
                            defaultValue="/content/plugins"
                    />
                    <div class="flex items-center space-x-2">
                        <Checkbox id="include" defaultChecked />
                        <label
                                for="include"
                                class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                        >
                            Allow administrators to change the directory.
                        </label>
                    </div>
                </form>
            </CardContent>
            <CardFooter class="border-t px-6 py-4">
                <Button>Save</Button>
            </CardFooter>
        </Card>
    </div>
</div>
