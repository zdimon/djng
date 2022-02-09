import {
    HttpEvent,
    HttpHandler,
    HttpInterceptor,
    HttpRequest,
  } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {SessionService} from './session.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
    token: string;
    language = 'en';

    constructor(
        private sessionService: SessionService,
    ) {
    }

    intercept(req: HttpRequest<any>,
              next: HttpHandler): Observable<HttpEvent<any>> {

        const idToken = this.sessionService.getToken();

        if (req.headers.get('Authorization') !== null) {
            return next.handle(req.clone());
        }
        // console.log(req.headers.get('Authorization').indexOf('Basic'));

        if (this.sessionService.getLanguage() === null) {
           this.sessionService.setLanguage('en');
         }

        const language = this.sessionService.getLanguage();

        if (idToken) {

            const cloned = req.clone({
                headers: req.headers.set('Authorization',
                    'Token ' + idToken)
                    .set('Accept-Language', language),
            });

            return next.handle(cloned);
        } else {
            const cloned = req.clone({
                headers: req.headers.set('Accept-Language', language),
            });
            return next.handle(cloned);
        }
    }
}
