export async function response_to_json(response) {
  const result = await response.json();
  return result;
}
