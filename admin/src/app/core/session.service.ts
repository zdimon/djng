
import {HttpClient} from '@angular/common/http';
import {Inject, Injectable} from '@angular/core';
import {Observable, of} from 'rxjs';
import {environment} from '../../environments/environment';

@Injectable()
export class SessionService {
  storage: any;
  constructor(  private http: HttpClient) {
    // this.storage = localStorage;
    this.storage = sessionStorage;
  }

  getToken(): string {
    return this.storage.getItem('access_token');
  }

  setToken(value: string) {
    this.storage.setItem('access_token', value);
  }

  removeToken() {
    this.storage.removeItem('access_token');
  }

  getSid(): string {
    return this.storage.getItem('socket_id');
  }

  setSid(value: string) {
    this.storage.setItem('socket_id', value);
  }

  getLanguage(): string {
    return this.storage.getItem('lang');
  }

  setLanguage(value: string) {
    this.storage.setItem('lang', value);
  }

  removeSid() {
    this.storage.removeItem('socket_id');
  }

  public get isLoggedIn(): Observable<boolean> {
    return of(this.storage.getItem('access_token') !== null);
  }

  public updateSocketId(data: any) {
    return this.http.post(`${environment.apiUrl}/online/update/socket/id`, data);
  }

  public addAccount(data: any) {
    return this.http.post(`${environment.apiUrl}/account/add`, data);
  }

  public setServerLanguage(language: string) {
    return this.http.get(`${environment.apiUrl}/account/setlanguage/${language}`);
  }

  public getOnlineCnt() {
    return this.http.get(`${environment.apiUrl}/online/count`);
  }

}
