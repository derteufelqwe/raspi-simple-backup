
export async function load({ params, fetch }) {
    const type = params.type;
    if (!["daily", "weekly", "monthly", "yearly"].includes(type)) {
        throw new Error("Invalid type value");
    }

    const request = await fetch('/api/files/' + type);
    const response = await request.json();

    return {
        'files': response.files,
    };
}
