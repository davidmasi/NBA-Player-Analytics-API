import {
  ChangeDetectorRef,
  Component,
  OnDestroy,
  OnInit,
  ViewEncapsulation
} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {untilDestroyed, UntilDestroy} from '@ngneat/until-destroy';
import {PlayersService} from '../_services/players.service';

@UntilDestroy()
@Component({
  selector: 'player-summary-component',
  templateUrl: './player-summary.component.html',
  styleUrls: ['./player-summary.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class PlayerSummaryComponent implements OnInit, OnDestroy {
  searchQuery: string = '';
  suggestions: any[] = [];
  playerSummary: any;

  constructor(
    protected activatedRoute: ActivatedRoute,
    protected cdr: ChangeDetectorRef,
    protected playersService: PlayersService,
  ) {}

  ngOnInit(): void {
    this.playersService.getPlayerSummary(1).pipe(untilDestroyed(this)).subscribe(data => {
      this.playerSummary = data.apiResponse;
      this.cdr.detectChanges();
    });
  }

  onSearch(): void {
    if (this.searchQuery.trim()) {
      this.playersService.searchPlayers(this.searchQuery)
        .pipe(untilDestroyed(this))
        .subscribe(results => {
          this.suggestions = results;
          this.cdr.detectChanges();
        });
    } else {
      this.suggestions = [];
    }
  }

  selectSuggestion(suggestion: any): void {
    this.searchQuery = suggestion.name;
    this.suggestions = [];
    this.playersService.getPlayerSummary(suggestion.id)
      .pipe(untilDestroyed(this))
      .subscribe({
        next: (data) => {
          this.playerSummary = data;
          this.cdr.detectChanges();
        },
        error: (error) => {
          console.error('Error fetching player summary:', error);
        }
      });
  }

  getXPosition(x: number): number {
    // Court width is 1455px
    const COURT_WIDTH = 1455;
    const COORDINATE_SCALE = 30;
    
    // Center the X coordinate and scale it
    const scaledX = x * COORDINATE_SCALE;
    const centeredX = (COURT_WIDTH / 2) + scaledX;
    
    return (centeredX / COURT_WIDTH) * 100;
  }

  getYPosition(y: number): number {
    // Court height is 1365px
    const COURT_HEIGHT = 1365;
    const COORDINATE_SCALE = 30;
    const BASKET_HEIGHT_FROM_BOTTOM = 140;
    
    // Transform Y coordinate relative to basket position
    const scaledY = y * COORDINATE_SCALE;
    const adjustedY = BASKET_HEIGHT_FROM_BOTTOM + scaledY;
    
    return (adjustedY / COURT_HEIGHT) * 100;
  }

  ngOnDestroy() {}
}