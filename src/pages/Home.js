import { useState } from 'react';
import Uploader from '../components/Uploader';
import Progress from '../components/Progress';
import Downloader from '../components/Downloader';


export function Home() {

  // 0 = initial state; 1 = uploaded; 2 = process completed; 3 = file downloaded
  const [status, setStatus] = useState(0);

  const renderSwitch = (param) => {
    switch(param) {
      case 0:
        return <Uploader setStatus={setStatus}/>
      case 1:
        return <Progress setStatus={setStatus}/>
      case 2:
        return <Downloader setStatus={setStatus}/>
      default:
        return <div>Thank you for using this app! See you next time!</div>
    }
  }

  return (
    <div>
      {renderSwitch(status)}
    </div>
  )
}
