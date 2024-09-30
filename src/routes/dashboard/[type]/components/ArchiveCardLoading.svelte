<script lang="ts">
    import {
        Card,
        CardHeader,
    } from "$lib/components/ui/card"
    import {Skeleton} from "$lib/components/ui/skeleton";
</script>


<Card class="border-gray-200">
    <CardHeader>
        <div class="flex flex-row gap-4 items-center">
            <Skeleton class="h-8 w-8 rounded-xl bg-gray-200"/>
            <Skeleton class="h-6 w-52 rounded-full bg-gray-200"/>
            <Skeleton class="h-6 w-16 rounded-full bg-gray-200"/>
            <Skeleton class="h-6 w-16 rounded-full bg-gray-200"/>
            <Skeleton class="h-8 w-8 rounded-md bg-gray-200 ml-auto"/>
        </div>
    </CardHeader>
</Card>
