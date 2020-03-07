export async function response_to_json(response) {
  console.log("util resp to json: ", response);
  const result = await response.json();
  return result;
}
