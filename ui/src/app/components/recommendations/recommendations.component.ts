import { Component, OnInit } from '@angular/core';
import { RecommendationService, Recommendation } from '../../services/recommendation.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-recommendations',
  templateUrl: './recommendations.component.html',
  styleUrls: ['./recommendations.component.scss']
})
export class RecommendationsComponent implements OnInit {
  customerId: string = 'DED5BF19E23CCCFEE322';
  recommendations: Recommendation[] = [];
  loading: boolean = false;
  requesting: boolean = false;

  constructor(
    private recommendationService: RecommendationService,
    private snackBar: MatSnackBar
  ) { }

  ngOnInit(): void {
    this.loadRecommendations();
  }

  requestRecommendations(): void {
    if (!this.customerId || this.customerId.trim() === '') {
      this.showMessage('Please enter a customer ID', 'error');
      return;
    }

    this.requesting = true;
    this.recommendations = [];

    this.recommendationService.requestRecommendations(this.customerId).subscribe({
      next: () => {
        this.showMessage('Recommendations requested! Loading...', 'success');
        // Wait a few seconds for processing, then load
        setTimeout(() => {
          this.loadRecommendations();
        }, 3000);
      },
      error: (error) => {
        this.requesting = false;
        this.showMessage('Error requesting recommendations: ' + (error.error?.detail || error.message), 'error');
        console.error('Error:', error);
      }
    });
  }

  loadRecommendations(): void {
    if (!this.customerId || this.customerId.trim() === '') {
      return;
    }

    this.loading = true;
    this.requesting = false;

    this.recommendationService.getRecommendations(this.customerId).subscribe({
      next: (response) => {
        this.recommendations = response.recommendations || [];
        this.loading = false;
        if (this.recommendations.length === 0) {
          this.showMessage('No recommendations found. Please request recommendations first.', 'info');
        }
      },
      error: (error) => {
        this.loading = false;
        this.showMessage('Error loading recommendations: ' + (error.error?.detail || error.message), 'error');
        console.error('Error:', error);
      }
    });
  }

  onAssetClick(recommendation: Recommendation): void {
    this.recommendationService.logInteraction(this.customerId, recommendation.isin, 'click').subscribe({
      next: () => {
        this.showMessage(`Clicked on ${recommendation.assetname}`, 'success');
      },
      error: (error) => {
        console.error('Error logging interaction:', error);
      }
    });
  }

  getProfitabilityColor(profitability: number): string {
    if (profitability > 0.1) return 'profit-high';
    if (profitability > 0) return 'profit-positive';
    if (profitability > -0.1) return 'profit-neutral';
    return 'profit-negative';
  }

  getProfitabilityIcon(profitability: number): string {
    if (profitability > 0) return 'trending_up';
    if (profitability < 0) return 'trending_down';
    return 'trending_flat';
  }

  formatPrice(price: number): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(price);
  }

  formatPercent(value: number): string {
    return (value * 100).toFixed(2) + '%';
  }

  getCategoryIcon(category: string): string {
    const icons: { [key: string]: string } = {
      'Stock': 'show_chart',
      'Bond': 'account_balance',
      'MTF': 'savings'
    };
    return icons[category] || 'pie_chart';
  }

  private showMessage(message: string, type: 'success' | 'error' | 'info'): void {
    this.snackBar.open(message, 'Close', {
      duration: 3000,
      horizontalPosition: 'right',
      verticalPosition: 'top',
      panelClass: [type === 'success' ? 'snackbar-success' : type === 'error' ? 'snackbar-error' : 'snackbar-info']
    });
  }
}

