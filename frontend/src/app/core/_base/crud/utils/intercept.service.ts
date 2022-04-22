import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest, HttpResponse } from '@angular/common/http';
// Angular
import { Injectable } from '@angular/core';
// RxJS
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { environment } from '../../../../../environments/environment';
import { SessionService } from './../../../session.service';
/**
 * More information there => https://medium.com/@MetonymyQT/angular-http-interceptors-what-are-they-and-how-to-use-them-52e060321088
 */
@Injectable()
export class InterceptService implements HttpInterceptor {
    // intercept request and add token
    constructor(private session_service: SessionService) {

    }
    intercept(
        request: HttpRequest<any>,
        next: HttpHandler,
    ): Observable<HttpEvent<any>> {
        // tslint:disable-next-line:no-debugger
        // modify request
        // request = request.clone({
        //  setHeaders: {
        //      Authorization: `Bearer ${localStorage.getItem('accessToken')}`
        //  }
        // });
        // console.log('----request----');
        // console.log(request);
        // console.log('--- end of request---');

        return next.handle(request).pipe(
            tap(
                event => {
                     if (event instanceof HttpResponse) {
                        // console.log('all looks good');
                        // http response status code
                        // console.log(event.status);
                    }
                },
                error => {
                    // http response status code
                    // console.log('----response----');
                    // console.error('status code:');
                    // tslint:disable-next-line:no-debugger
                    if (error.status === 401) {
                        this.session_service.removeToken();
                        localStorage.removeItem(environment.authTokenKey);
                    }
                    console.error(error.status);
                    console.error(error.message);
                    
                },
            ),
        );
    }
}
