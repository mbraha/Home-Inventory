export async function get_new_access_token(token) {
  let result = null;
  try {
    const response = await fetch("http://127.0.0.1:5000/token/refresh", {
      method: "POST",
      headers: new Headers({ Authorization: "Bearer " + token })
    });
    result = await response.json();
    console.log("get_new_access_token result", result);
  } catch (error) {
    console.log("get_new_access_token error", error);
  }

  return result;
}
