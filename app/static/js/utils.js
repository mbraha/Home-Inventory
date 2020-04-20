/*
These functions give the React frontend access to our API.
They only obtain the information. Callers should handle using the data.
*/
async function perform_fetch({
  endpoint,
  method = "POST",
  query = "",
  headers = new Headers(),
} = {}) {
  /*
  Custom Wrapper for fetch() to interact with our API.

  Return result object on success, null if fetch failed, HTTP error code otherwise.
  */
  try {
    const response = await fetch(
      "http://127.0.0.1:5000/" + endpoint + "?" + query,
      {
        method: method,
        headers: headers,
      }
    );
    if (response.status == 200) {
      const result = await response.json();
      console.log(`fetch success: ${method} ${endpoint}`, result);
      return result;
    } else {
      console.log(`fetch error: ${method} ${endpoint}`, response);
      return response.status;
    }
  } catch (error) {
    console.log(`fetch error: ${method} ${endpoint}`, error);
    return null;
  }
}

export async function get_new_access_token(token) {
  const header = new Headers({ Authorization: "Bearer " + token });
  return await perform_fetch({
    endpoint: "token/refresh",
    headers: header,
  });
  // try {
  //   const response = await fetch("http://127.0.0.1:5000/token/refresh", {
  //     method: "POST",
  //     headers: new Headers({ Authorization: "Bearer " + token }),
  //   });
  //   console.log("get_new_access_token response", response);
  //   if (response.status == 200) {
  //     const result = await response.json();
  //     return result;
  //   } else {
  //     return response.status;
  //   }
  // } catch (error) {
  //   console.log("get_new_access_token error", error);
  // }
}

export async function full_logout(access_token, refresh_token) {
  const acc_header = new Headers({ Authorization: "Bearer " + access_token });
  const ref_header = new Headers({ Authorization: "Bearer " + refresh_token });
  const acc_response = perform_fetch({
    endpoint: "logout/access",
    headers: acc_header,
  });
  const ref_response = perform_fetch({
    endpoint: "logout/refresh",
    headers: ref_header,
  });
  if (acc_response && ref_response) {
    console.log("logout success");
    return true;
  } else {
    console.log("logout failure", error);
    return false;
  }
  // try {
  // const acc_response = await fetch("http://127.0.0.1:5000/logout/access", {
  //   method: "POST",
  //   headers: new Headers({ Authorization: "Bearer " + access_token }),
  // });
  // const ref_response = await fetch("http://127.0.0.1:5000/logout/refresh", {
  //   method: "POST",
  //   headers: new Headers({ Authorization: "Bearer " + refresh_token }),
  // });
  //   if (acc_response.status === 200 && ref_response.status === 200) {
  //     console.log("logout success");
  //     return true;
  //   }
  // } catch (error) {
  //   console.log("logout failure", error);
  //   return false;
  // }
}

export async function get_users() {
  return await perform_fetch({ endpoint: "users", method: "GET" });
}

export async function add_room(owner, room_name) {
  const query = "owner=" + owner + "room_name=" + room_name;
  return await perform_fetch({ endpoint: "room", query: query });
  // try {
  //   const query = "owner=" + owner + "room_name=" + room_name;
  //   const response = await fetch("http://127.0.0.1:5000/add_room?" + query, {
  //     method: "POST",
  //   });
  //   if (response.status == 200) {
  //     const result = await response.json();
  //     return result;
  //   } else {
  //     return response.status;
  //   }
  // } catch (error) {
  //   console.log("add_room failure", error);
  //   return null;
  // }
}
