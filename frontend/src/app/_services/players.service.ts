import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PlayersService {
  private apiUrl = 'http://localhost:3000'; // adjust if your backend URL is different

  constructor(private http: HttpClient) {}

  getPlayerSummary(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/players/${id}`);
  }

  searchPlayers(query: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/players/search?q=${query}`);
  }
}