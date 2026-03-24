const { use } = require("react");

const API = "http://127.0.0.1:8000/users";

async function uploadNhanSu(event) {
  event.preventDefault(); 
  const formData = new FormData(event.target);

  try {
      const res = await axios.post('http://127.0.0.1:8000/nhansu/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
      });
          
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
  const response = await fetch(API);
  const users = await response.json();

  const container = document.getElementById("list_user");
  users.forEach((user) => {
    const row = document.createElement("tr");

    row.onclick = function () {
      window.location.href = "profileuser.html?id=" + user.id;
    };

    row.innerHTML = `
    <td>${user.name}</td>
    <td>${user.email}</td>
    <td>${user.donvi}</td>
    <td>
        <span onclick="editUser()">Edit</span>
    </td>
    <td>
        <span onclick="deleteUser(${user.id})>X</span>
    </td>`;
    container.appendChild(row);
  });
}



async function loadUser() {
  const id = getUserId();
  if (!id) return;
  const res = await fetch("/users/" + id);
  const user = await res.json();

  document.getElementById("email").innerText = user.email;
  document.getElementById("name").innerText = user.name;
  document.getElementById("gioitinh").innerText = user.gioitinh;
  document.getElementById("trinhdo").innerText = user.trinhdo;
  document.getElementById("donvi").innerText = user.donvi;
  document.getElementById("hocham").innerText = user.hocham;

  document.getElementById("avatar").src = user.hinhanh;
}


async function deleteUser(id) {
  if (!confirm("Xóa nhân sự này?")) return;

  await fetch(API + "/" + id, {
    method: "DELETE",
  });

  loadListUser();
}

function editUser() {
  const params = new URLSearchParams(window.location.search);
  const id = params.get("id");

  window.location.href = "editProfile.html?id=" + id;
}

async function loadUserToEdit() {
  const id = getUserId();
  if (!id) return;

  const res = await fetch("http://127.0.0.1:8000/users/" + id);
  const user = await res.json();

  document.getElementById("email").value = user.email;
  document.getElementById("name").value = user.name;
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

  await fetch("http://127.0.0.1:8000/users/" + id, {
    method: "PUT",
    body: formData,
  });

  alert("Cập nhật thành công");

  window.location.href = "user_detail.html?id=" + id;
}

window.onload = function () {
  if (document.getElementById("editForm")) {
    loadUserToEdit();
    document.getElementById("editForm").addEventListener("submit", updateUser);
  }
};
