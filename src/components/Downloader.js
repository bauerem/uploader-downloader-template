const Downloader = function () {

    const onClick = async (ev) => {
        ev.preventDefault();
        const response = await fetch('/api/download');
        const blob = await response.blob();
        const url = window.URL.createObjectURL(new Blob([blob]));
        const link = document.createElement('a');
        const token = document.cookie.replace("token=","");
        link.href = url;
        link.setAttribute('download', token);
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);
    }

    return (
      <button onClick={onClick}>Download</button>
    )
  }

export default  Downloader;