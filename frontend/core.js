const API = "http://127.0.0.1:8000";

async function loginUser(event) {
  event.preventDefault();

  email = document.getElementById("email").value;
  matkhau = document.getElementById("password").value;

  bodyData = {
    email: email,
    matkhau: matkhau,
  };
  try {
    const res = await fetch("http://127.0.0.1:8000/user/login", {
      method: "POST",
      body: JSON.stringify(bodyData),
      headers: { "Content-type": "application/json; charset=UTF-8" },
    });
    const data = await res.json();
    if (res.ok) {
      alert(data.detail);
      localStorage.setItem("user", data.name);
      window.location.href = "listUser.html";
    } else {
      alert("Lỗi: " + data.detail);
    }
  } catch (err) {
    console.error(err.detail);
  }
}

async function uploadNhanSu(event) {
  event.preventDefault();
  const formData = new FormData(event.target);

  try {
    const res = await axios.post(
      "http://127.0.0.1:8000/nhansu/upload",
      formData,
      {
        headers: { "Content-Type": "multipart/form-data" },
      },
    );

    alert(res.data.msg);
    event.target.reset();
  } catch (err) {
    console.error(err);
    const detail = err.response?.data?.detail;
    alert("Lỗi: " + JSON.stringify(detail));
  }
}

function getUserId() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

async function loadListUser() {
  const response = await fetch("http://127.0.0.1:8000/nhansu/general_info");
  const users = await response.json();

  const container = document.getElementById("list_user");
  users.forEach((user) => {
    const row = document.createElement("tr");

    row.onclick = function () {
      window.location.href = "profileuser.html?id=" + user.id;
    };

    row.innerHTML = `
    <td><img src="${user.image_data}" width="50"/></td>
    <td>${user.hoten}</td>
    <td>${user.email}</td>
    <td>${user.donvi}</td>
    <td>
        <button onclick="event.stopPropagation(); editUser(${user.id})">Edit</button>
    </td>
    <td>
        <button onclick="event.stopPropagation(); deleteUser(${user.id})">X</button>
    </td>`;
    container.appendChild(row);
  });
}

async function loadList() {
  const response = await fetch("http://127.0.0.1:8000/nhansu/general_info");
  const users = await response.json();

  const container = document.getElementById("list");
  users.forEach((user) => {
    const div = document.createElement("div");
    div.classList.add("card");
    div.innerHTML = `
    <img src="${user.image_data}" width="100"/>
    <div class="card-content">
      <h3>${user.hoten}</h3>
      <p class="email">${user.email}</p>
      <p>Đơn vị: ${user.donvi}</p>
    </div>`;
    container.appendChild(div);
  });
}

async function loadUser() {
  const id = getUserId();
  if (!id) return;
  const res = await fetch("http://127.0.0.1:8000/nhansu/detail_info?id=" + id);
  const user = await res.json();

  document.getElementById("email").innerText = user.email;
  document.getElementById("name").innerText = user.hoten;
  document.getElementById("gioitinh").innerText = user.gioitinh;
  document.getElementById("trinhdo").innerText = user.trinhdo;
  document.getElementById("donvi").innerText = user.donvi;
  document.getElementById("hocham").innerText = user.hocham;
}

async function deleteUser(id) {
  if (!confirm("Xóa nhân sự này?")) return;

  await fetch("http://127.0.0.1:8000/nhansu/delete?id=" + id, {
    method: "DELETE",
  });

  //loadListUser();
  window.location.reload();
}

function editUser(id) {
  const params = new URLSearchParams(window.location.search);
  // const id = params.get("id");

  window.location.href = "editProfile.html?id=" + id;
}

async function loadUserToEdit() {
  const id = getUserId();
  if (!id) return;
  console.log("ID" + id);

  const res = await fetch("http://127.0.0.1:8000/nhansu/detail_info?id=" + id);
  const user = await res.json();

  document.getElementById("email").value = user.email;
  document.getElementById("name").value = user.hoten;
  document.getElementById("trinhdo").value = user.trinhdo;
  document.getElementById("donvi").value = user.donvi;
  document.getElementById("hocham").value = user.hocham;

  // set radio giới tính
  const radios = document.getElementsByName("gioitinh");
  radios.forEach((r) => {
    if (r.value === user.gioitinh) {
      r.checked = true;
    }
  });
}

async function updateUser(event) {
  event.preventDefault();

  const id = getUserId();

  const form = document.getElementById("editForm");

  const formData = new FormData(form);

  await fetch("http://127.0.0.1:8000/nhansu/update?id=" + id, {
    method: "POST",
    body: formData,
  });

  alert("Cập nhật thành công");

  window.location.href = "profileuser.html?id=" + id;
}

window.onload = function () {
  if (document.getElementById("editForm")) {
    loadUserToEdit();
    document.getElementById("editForm").addEventListener("submit", updateUser);
  }
};
