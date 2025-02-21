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
  // Add these properties
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

  // Add these methods
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
      .subscribe(data => {
        this.playerSummary = data.apiResponse;
        this.cdr.detectChanges();
      });
  }

  ngOnDestroy() {}
}