export function getCookiesMap(cookiesString) {
    return cookiesString.split(";")
      .map(function(cookieString) {
          return cookieString.trim().split("=");
      })
      .reduce(function(acc, curr) {
          acc[curr[0]] = curr[1];
          return acc;
      }, {});
  }