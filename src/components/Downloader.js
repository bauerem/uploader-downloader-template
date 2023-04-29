import { getCookiesMap } from "../helpers/getCookiesMap";

const Downloader = function ({setStatus}) {

    const onClick = async (ev) => {
        ev.preventDefault();
        const response = await fetch('/api/download');
        const blob = await response.blob();
        const url = window.URL.createObjectURL(new Blob([blob]));
        const link = document.createElement('a');

        const cookies = getCookiesMap(document.cookie);
        const local_filename = cookies['filename'];
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

export default  Downloader;