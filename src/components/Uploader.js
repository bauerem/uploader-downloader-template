import { useState } from 'react';
import { Box } from '@chakra-ui/react';


const  Uploader = ({setStatus}) => {
    const [uploading, setUploading] = useState(false);
  
    const onSubmit = async (ev) => {
      ev.preventDefault();
      const formData = new FormData();
      formData.append('inputFile', ev.target.inputFile.files[0]);
      setUploading(true);
      const response = await fetch("/api/upload", {
        method: 'POST',
        body: formData
      });
      if (response.ok) {
        console.log("Post sent!");
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

export default  Uploader;