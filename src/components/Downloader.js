import { api } from "../helpers/api";

const Downloader = function ({ setStatus }) {

  const onClick = async (ev) => {
    ev.preventDefault();
    const data = {
      "token": localStorage.getItem("token")
    }

    const response = await fetch(api + "/api/download", {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data)
    });

    const blob = await response.blob();
    const url = window.URL.createObjectURL(new Blob([blob]));
    console.log(url);
    const link = document.createElement('a');

    //const cookies = getCookiesMap(document.cookie);
    //const local_filename = cookies['filename'];
    const local_filename = localStorage.getItem("local_filename")
    link.href = url;
    link.setAttribute('download', local_filename);
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
    setStatus(3);
  }

  return (
    <button onClick={onClick}>Download</button>
  )
}

export default Downloader;