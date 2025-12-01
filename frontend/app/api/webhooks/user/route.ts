import { NextResponse } from "next/server";
import { Webhook } from "svix";
import {prisma} from "@/lib/prisma";

const webhookSecret = process.env.CLERK_WEBHOOK_SECRET!;

export async function POST(req: Request) {
  const payload = await req.text();

  const svixId = req.headers.get("svix-id")!;
  const svixTimestamp = req.headers.get("svix-timestamp")!;
  const svixSignature = req.headers.get("svix-signature")!;

  const wh = new Webhook(webhookSecret);
  let evt: any;

  try {
    evt = wh.verify(payload, {
      "svix-id": svixId,
      "svix-timestamp": svixTimestamp,
      "svix-signature": svixSignature,
    });
  } catch {
    return new NextResponse("Webhook Error", { status: 400 });
  }

  const {
    id: clerkId,
    email_addresses,
    first_name,
    last_name,
    image_url,
  } = evt.data;

  if (!clerkId) {
    return new NextResponse("Missing clerkId", { status: 400 });
  }

  const email = email_addresses?.[0]?.email_address || "";
  const fullName = `${first_name || ""} ${last_name || ""}`.trim();

  try {
    await prisma.user.upsert({
      where: { clerkId },
      update: {
        email,
        fullName,
        imageUrl: image_url || "",
      },
      create: {
        clerkId,
        email,
        fullName,
        imageUrl: image_url || "",
      },
    });

    return NextResponse.json({ success: true });
  } catch {
    return new NextResponse("Database Error", { status: 500 });
  }
}
