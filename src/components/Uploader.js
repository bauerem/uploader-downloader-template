import { useState } from 'react';
import { Box } from '@chakra-ui/react';
import { api } from "../helpers/api";

const Uploader = ({ setStatus }) => {
  const [uploading, setUploading] = useState(false);

  const onSubmit = async (ev) => {
    ev.preventDefault();

    const formData = new FormData();
    formData.append('inputFile', ev.target.inputFile.files[0]);

    setUploading(true);

    // Upload file
    const response = await fetch(api + "/api/upload", {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      console.log("Post sent!");

      // Store filename and token
      const response_data = await response.json()
      localStorage.setItem("token", response_data["token"])
      localStorage.setItem("local_filename", response_data["filename"])

      setUploading(false);
      setStatus(1); // status numbers defined in parent component
    }
  }

  return (
    <form onSubmit={onSubmit}>
      <input id="inputFile" type="file" />
      {uploading ? <div>Uploading...</div> : <button><Box>Submit</Box></button>}
    </form>
  )
}

export default Uploader;