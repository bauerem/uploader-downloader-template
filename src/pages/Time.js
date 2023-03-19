import { useState, useEffect } from 'react';

export function Time() {
  const [currentTime, setCurrentTime] = useState(1);

  useEffect(() => {
    fetch("api/time").then(res => res.json()).then(data => {
      setCurrentTime(data.time)
    })
  }, []);
  return (
    <p>The current time is {currentTime}.</p>
  )
}
