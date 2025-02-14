function arrayBufferToBase64(buffer) {
  const bytes = buffer instanceof Uint8Array ? buffer : new Uint8Array(buffer);
  let binary = "";
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return window.btoa(binary);
}

function base64ToArrayBuffer(base64) {
  const binary = window.atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes.buffer;
}

async function importKey(rawKey) {
  return window.crypto.subtle.importKey("raw", rawKey, "AES-GCM", true, [
    "encrypt",
    "decrypt",
  ]);
}

export async function getKey() {
  const constantKey = "dGhpc2lzYXN0cm9uZ3NlY3JldGtleWZvcnRlc3Rpbmc=";
  const raw = base64ToArrayBuffer(constantKey);
  return importKey(raw);
}

export async function encryptMessage(plaintext) {
  const key = await getKey();
  const iv = window.crypto.getRandomValues(new Uint8Array(12));
  const encoder = new TextEncoder();
  const encoded = encoder.encode(plaintext);
  const ciphertextBuffer = await window.crypto.subtle.encrypt(
    { name: "AES-GCM", iv: iv },
    key,
    encoded
  );
  const ciphertext = arrayBufferToBase64(ciphertextBuffer);
  const ivStr = arrayBufferToBase64(iv);
  return { ciphertext, iv: ivStr };
}

export async function decryptMessage(ciphertext, ivStr) {
  const key = await getKey();
  const ivBuffer = base64ToArrayBuffer(ivStr);
  const ciphertextBuffer = base64ToArrayBuffer(ciphertext);
  const ivArray = new Uint8Array(ivBuffer);
  console.log("Decryption: IV length:", ivArray.length);
  try {
    const decryptedBuffer = await window.crypto.subtle.decrypt(
      { name: "AES-GCM", iv: ivArray },
      key,
      ciphertextBuffer
    );
    const decoder = new TextDecoder();
    return decoder.decode(decryptedBuffer);
  } catch (err) {
    console.error(
      "Decryption failed. IV (Base64):",
      ivStr,
      "IV Array:",
      ivArray,
      "Ciphertext Buffer:",
      new Uint8Array(ciphertextBuffer)
    );
    throw err;
  }
}
