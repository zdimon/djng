// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  production: false,
  isMockEnabled: false, // You have to switch this, when your real back-end is done
  authTokenKey: 'authce9d77b308c149d5992a80073637e4d5',
  apiUrl: 'http://localhost:8085',
  socketUrl: 'http://localhost:8889',
  OPENVIDU_SERVER_URL: 'https://dating-test.webmonstr.com:4443',
  OPENVIDU_SERVER_SECRET: 'SECRET',
  AGM_KEY: 'AIzaSyAPwNh3548jURbTa7tUYCuk4Odf7qVxeCM',
  GOOGLE_AUTH: '228193226064-3pcced1cqkk21hdgngai7s89o6galqgr.apps.googleusercontent.com',
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.
