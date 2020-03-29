export async function get_new_access_token(token) {
  try {
    const response = await fetch("http://127.0.0.1:5000/token/refresh", {
      method: "POST",
      headers: new Headers({ Authorization: "Bearer " + token })
    });
    console.log("get_new_access_token response", response);
    if (response.status == 200) {
      const result = await response.json();
      return result;
    } else {
      return response.status;
    }
  } catch (error) {
    console.log("get_new_access_token error", error);
  }
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

export async function get_users() {
  try {
    const response = await fetch("http://127.0.0.1:5000/users", {
      method: "GET"
    });
    if (response.status == 200) {
      const result = await response.json();
      return result;
    } else {
      return response.status;
    }
  } catch (error) {
    console.log("get users failure", error);
    return null;
  }
}

export async function add_room(owner, room_name) {
  try {
    const query = "owner=" + owner + "room_name=" + room_name;
    const response = await fetch("http://127.0.0.1:5000/add_room?" + query, {
      method: "POST"
    });
    if (response.status == 200) {
      const result = await response.json();
      return result;
    } else {
      return response.status;
    }
  } catch (error) {
    console.log("add_room failure", error);
    return null;
  }
}
