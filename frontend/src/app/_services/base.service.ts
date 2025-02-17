import * as _ from 'lodash';

import {HttpClient, HttpHeaders, HttpParams, HttpResponse, HttpParameterCodec} from '@angular/common/http';
import {Observable, throwError} from 'rxjs';
import {catchError} from 'rxjs/operators';

export class BaseService {

  protected get headers(): HttpHeaders {
    return new HttpHeaders();
  }

  errorKeyMap: any = {};

  protected baseUrl = window.location.origin.includes('localhost') ? 'http://localhost:8000/api/v1' : (window.location.origin + '/api/v1');
  protected defaultLimit: number = 25;

  constructor(protected http: HttpClient) {}

  protected get(url: string, params?: HttpParams): Observable<any> {
    const options = {headers: this.headers, params: params};

    return this.http.get(url, options).pipe(catchError(this.getErrorHandler()));
  }

  protected post(url: string, data: {}, params?: HttpParams): Observable<any> {
    const options = {headers: this.headers};

    return this.http.post(url, data, options).pipe(catchError(this.getErrorHandler()));
  }

  protected put(url: string, data: {}, options?: any): Observable<any> {
    options = options || {headers: this.headers};

    return this.http.put(url, data, options).pipe(catchError(this.getErrorHandler()));
  }

  protected patch(url: string, data: {}, options?: any): Observable<any> {
    options = options || {headers: this.headers};

    return this.http.patch(url, data, options).pipe(catchError(this.getErrorHandler()));
  }

  protected delete(url: string, options?: any): Observable<any> {
    return this.http.delete(url, options).pipe(catchError(this.getErrorHandler()));
  }

  protected getErrorHandler() {
    return res => {
      if (res.status === 401) {
      }

      const errorPairs: [string, string][] = _(res.error).toPairs().value();
      const errorMessages: string[] = errorPairs.map(error => {
        const keyName: string = this.errorKeyMap[error[0]] || error[0];
        return `${keyName}: ${error[1]}`;
      });

      return throwError(<HttpErrorResponse>{
        status: res.status,
        response: res,
        errorMessages: errorMessages
      });
    };
  }
}

export class HttpErrorResponse {
  status: number;
  response: HttpResponse<any>;
  errorMessages: string[];
}

export class CustomHttpParamEncoder implements HttpParameterCodec {
  // Use this class when you want to encode any of: '@', ':', '$', ',', ';', '+', '=', '?', '/' in the query parameters of an HTTP request
  // Usage: let params: HttpParams = new HttpParams({ encoder: new CustomHttpParamEncoder() })
  // Example use case: Query parameter with a timestamp in UTC+ timezone. Django will interpret the '+' as a space if not encoded as '%2b%'
  // Default Angular behavior is to not encode these characters in order to comply with RFC 3986
  // See https://github.com/angular/angular/blame/540c29cd6bfc4124a30f5f8e7b599d326baf6af4/packages/common/http/src/params.ts#L90

  encodeKey(key: string): string {
    return encodeURIComponent(key);
  }
  encodeValue(value: string): string {
    return encodeURIComponent(value);
  }
  decodeKey(key: string): string {
    return decodeURIComponent(key);
  }
  decodeValue(value: string): string {
    return decodeURIComponent(value);
  }
}
