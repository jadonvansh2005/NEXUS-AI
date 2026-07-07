const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function sendChatMessage(
  message: string,
  file?: File
) {

  const formData =
    new FormData();

  formData.append(
    "message",
    message
  );

  if (file) {

    formData.append(
      "file",
      file
    );

  }

  const response =
    await fetch(

      `${API_URL}/chat`,

      {

        method: "POST",

        body:
          formData

      }

    );

  if (
    !response.ok
  ) {

    throw new Error(
      `API Error ${response.status}`
    );

  }

  return response.json();

}