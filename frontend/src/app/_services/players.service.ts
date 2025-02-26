import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PlayersService {
  private apiUrl = 'http://localhost:8000/api/v1';

  constructor(private http: HttpClient) {}

  getPlayerSummary(playerId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/playerSummary/${playerId}/`);
  }

  searchPlayers(query: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/playerSearch/`, {
      params: { query }
    });
  }
}