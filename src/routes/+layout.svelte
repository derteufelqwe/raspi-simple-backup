<script>
    import "../app.css";
    import {
        DropdownMenu, DropdownMenuContent,
        DropdownMenuItem, DropdownMenuLabel,
        DropdownMenuSeparator,
        DropdownMenuTrigger
    } from "$lib/components/ui/dropdown-menu";
    import {Link} from "$lib/link";
    import {Button} from "$lib/components/ui/button";
    import {
        Card,
        CardContent,
        CardDescription,
        CardFooter,
        CardHeader,
        CardTitle
    } from "$lib/components/ui/card";
    import {CircleUser, Menu, Package2, Search, ServerCog} from "lucide-svelte";
    import {Sheet, SheetContent, SheetTrigger} from "$lib/components/ui/sheet";
    import {Input} from "$lib/components/ui/input";
    import {Checkbox} from "$lib/components/ui/checkbox";
</script>


<div class="flex min-h-screen w-full flex-col">
    <header class="sticky top-0 flex h-16 items-center gap-4 border-b bg-background px-4 md:px-6">
        <nav class="hidden flex-col gap-6 text-lg font-medium md:flex md:flex-row md:items-center md:gap-5 md:text-sm lg:gap-6">
            <Link
                    href="#"
                    class="flex items-center gap-2 text-lg font-semibold md:text-base"
            >
                <ServerCog class="h-7 w-7" />
                <span class="sr-only">Server Backups</span>
            </Link>
            <Link href="#" class="whitespace-nowrap text-lg">Backups Dashboard</Link>
        </nav>
        <Sheet>
            <SheetTrigger asChild let:builder>
                <Button
                        variant="outline"
                        size="icon"
                        class="shrink-0 md:hidden"
                        builders={[builder]}
                >
                    <Menu class="h-5 w-5" />
                    <span class="sr-only">Toggle navigation menu</span>
                </Button>
            </SheetTrigger>
            <SheetContent side="left">
                <nav class="grid gap-6 text-lg font-medium">
                    <Link
                            href="#"
                            class="flex items-center gap-2 text-lg font-semibold"
                    >
                        <ServerCog class="h-7 w-7" />
                        <span class="sr-only">Server Backups</span>
                    </Link>
                    <hr>
                    <Link href="#">Backups Dashboard</Link>
                </nav>
            </SheetContent>
        </Sheet>
        <div class="flex w-full items-center gap-4 md:ml-auto md:gap-2 lg:gap-4">
<!--            <form class="ml-auto flex-1 sm:flex-initial">-->
<!--                <div class="relative">-->
<!--                    <Search class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />-->
<!--                    <Input-->
<!--                            type="search"-->
<!--                            placeholder="Search products..."-->
<!--                            class="pl-8 sm:w-[300px] md:w-[200px] lg:w-[300px]"-->
<!--                    />-->
<!--                </div>-->
<!--            </form>-->
<!--            <DropdownMenu>-->
<!--                <DropdownMenuTrigger asChild let:builder>-->
<!--                    <Button variant="secondary" size="icon" class="rounded-full" builders={[builder]}>-->
<!--                        <CircleUser class="h-5 w-5" />-->
<!--                        <span class="sr-only">Toggle user menu</span>-->
<!--                    </Button>-->
<!--                </DropdownMenuTrigger>-->
<!--                <DropdownMenuContent align="end">-->
<!--                    <DropdownMenuLabel>My Account</DropdownMenuLabel>-->
<!--                    <DropdownMenuSeparator />-->
<!--                    <DropdownMenuItem>Settings</DropdownMenuItem>-->
<!--                    <DropdownMenuItem>Support</DropdownMenuItem>-->
<!--                    <DropdownMenuSeparator />-->
<!--                    <DropdownMenuItem>Logout</DropdownMenuItem>-->
<!--                </DropdownMenuContent>-->
<!--            </DropdownMenu>-->
        </div>
    </header>

    <main class="flex min-h-[calc(100vh_-_theme(spacing.16))] flex-1 flex-col gap-4 bg-muted/40 p-4 md:gap-8 md:p-10">
        <slot/>
    </main>
</div>
