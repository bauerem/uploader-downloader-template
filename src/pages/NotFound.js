import { useNavigate } from "react-router-dom";

export function NotFound() {
  const navigate = useNavigate()
  setTimeout(() => {
    navigate(-1)
  }, 3000)
  return <h1>404 Error: Page Not Found. You will be redirected shortly.</h1>
}
