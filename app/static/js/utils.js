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

export async function full_logout(access_token, refresh_token) {
  try {
    const acc_response = await fetch("http://127.0.0.1:5000/logout/access", {
      method: "POST",
      headers: new Headers({ Authorization: "Bearer " + access_token })
    });
    const ref_response = await fetch("http://127.0.0.1:5000/logout/refresh", {
      method: "POST",
      headers: new Headers({ Authorization: "Bearer " + refresh_token })
    });
    if (acc_response.status === 200 && ref_response.status === 200) {
      console.log("logout success");
      return true;
    }
  } catch (error) {
    console.log("logout failure", error);
    return false;
  }
}
