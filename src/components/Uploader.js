import { useState } from 'react';

const  Uploader = () => {
    const [loading, setLoading] = useState(false);
  
    const onSubmit = async (ev) => {
      ev.preventDefault();
      const formData = new FormData();
      formData.append('inputFile', ev.target.inputFile.files[0]);
      setLoading(true);
      const response = await fetch("/api/upload", {
        method: 'POST',
        body: formData
      });
      if (response.ok) {
        console.log("Post sent!");
        setLoading(false);
      }
    }
    
    return (
      <form onSubmit={onSubmit}>
        <input id="inputFile" type="file" />
        {loading ? <div>Loading...</div> : <button>Submit</button>}
      </form>
    )
  }

export default  Uploader;