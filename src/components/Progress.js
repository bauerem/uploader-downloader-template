import { useState, useEffect } from 'react';


const Progress = () => {

    const [data, setData] = useState('Processing...');

    useEffect(() => {
        const token = document.cookie.match(/token=([^;]+)/)[1]; // extract token value from cookie
        const sse = new EventSource(`http://localhost:5000/api/stream?token=${token}`);

        function handleStream(e) {
            console.log(e);
            setData(e);
        }

        sse.onmessage = e => (handleStream(e.data));

        sse.onerror = e => {
            // DON'T DEPLOY LIKE THIS
            // will stall and stop stream
            sse.close();
        }

    }, []);

    return (
        <div>
            <p>
                The time is : {data}
            </p>
        </div>
    )

}


export default  Progress;