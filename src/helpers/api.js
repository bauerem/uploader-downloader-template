let api = 'http://localhost:5000';

if (process.env.NODE_ENV == "production") {
    api = "http://ec2-3-74-162-50.eu-central-1.compute.amazonaws.com";
}

export { api };