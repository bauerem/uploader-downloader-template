import { Spinner } from '@chakra-ui/react';
import { useState, useEffect } from 'react';

const Progress = ({setStatus}) => {

    const [data, setData] = useState(false);

    useEffect(() => {
        const token = document.cookie.match(/token=([^;]+)/)[1]; // extract token value from cookie
        const sse = new EventSource(`http://localhost:5000/api/stream?token=${token}`);

        function handleStream(e) {
            if (e === 'done') {
                setData(true);
                sse.close();
                setStatus(2); // status numbers defined in parent component
            }
        }

        sse.onmessage = e => (handleStream(e.data));

        sse.onerror = e => {
            // DON'T DEPLOY LIKE THIS
            // will stall and stop stream
            sse.close();
        }
    }, [setStatus]);

    const done = <p>done</p>;

    return (
        <div>
                {data ?  done: <Spinner size='xl' />}
        </div>
    )

}


export default  Progress;