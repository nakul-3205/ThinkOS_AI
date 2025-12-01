import { NextResponse } from "next/server";
import crypto from "crypto";

const PY_BACKEND_URL = process.env.PY_BACKEND_URL!;
const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY!;

function encrypt(text: string) {
const iv = crypto.randomBytes(12);
const cipher = crypto.createCipheriv("aes-256-gcm", Buffer.from(ENCRYPTION_KEY), iv);

let encrypted = cipher.update(text, "utf8", "base64");
encrypted += cipher.final("base64");

const authTag = cipher.getAuthTag().toString("base64");

return { iv: iv.toString("base64"), authTag, encrypted };
}

export async function POST(req: Request) {
try {
const { userId, chatId, prompt } = await req.json();
if (!userId || !chatId || !prompt) {
    return NextResponse.json({ error: "Missing fields" }, { status: 400 });
}

const encrypted = encrypt(JSON.stringify({ userId, chatId, prompt }));


fetch(`${PY_BACKEND_URL}/process`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(encrypted),
}).catch(() => {});

return NextResponse.json({ success: true });
} catch {
return NextResponse.json({ error: "Server error" }, { status: 500 });
}
}
