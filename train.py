"""
Standalone training script for ATK Classifier.
Can be run from command line to train models.

Usage:
    python train.py dataset_alat_tulis --simple
    python train.py dataset_alat_tulis --tune --epochs 25 --trials 10
"""
import argparse
import sys
from pathlib import Path

from models.train_model import ATKModelTrainer


def main():
    parser = argparse.ArgumentParser(description='Train ATK Classifier Model')
    
    parser.add_argument(
        'dataset_dir',
        type=str,
        help='Path to dataset directory containing class folders'
    )
    
    parser.add_argument(
        '--tune',
        action='store_true',
        help='Use hyperparameter tuning (slower but better results)'
    )
    
    parser.add_argument(
        '--epochs',
        type=int,
        default=15,
        help='Number of training epochs (default: 15)'
    )
    
    parser.add_argument(
        '--trials',
        type=int,
        default=10,
        help='Number of tuning trials (only with --tune, default: 10)'
    )
    
    parser.add_argument(
        '--img-size',
        type=int,
        default=300,
        choices=[224, 300],
        help='Input image size (default: 300)'
    )
    
    parser.add_argument(
        '--batch-size',
        type=int,
        default=15,
        help='Batch size for training (default: 15)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='models/best_model.h5',
        help='Output path for trained model (default: models/best_model.h5)'
    )
    
    args = parser.parse_args()
    
    # Validate dataset directory
    if not Path(args.dataset_dir).exists():
        print(f"Error: Dataset directory '{args.dataset_dir}' not found")
        sys.exit(1)
    
    print("=" * 60)
    print("ATK Classifier Model Training")
    print("=" * 60)
    print(f"Dataset: {args.dataset_dir}")
    print(f"Mode: {'Hyperparameter Tuning' if args.tune else 'Simple Training'}")
    print(f"Epochs: {args.epochs}")
    print(f"Image Size: {args.img_size}x{args.img_size}")
    print(f"Batch Size: {args.batch_size}")
    if args.tune:
        print(f"Tuning Trials: {args.trials}")
    print(f"Output: {args.output}")
    print("=" * 60)
    print()
    
    # Initialize trainer
    trainer = ATKModelTrainer(
        dataset_dir=args.dataset_dir,
        img_height=args.img_size,
        img_width=args.img_size,
        batch_size=args.batch_size
    )
    
    # Prepare dataset
    print("Loading dataset...")
    class_names = trainer.prepare_dataset()
    print(f"Classes: {class_names}")
    print()
    
    # Train model
    if args.tune:
        print("Starting hyperparameter tuning...")
        model, history, best_hps = trainer.train_with_tuning(
            max_epochs=args.epochs,
            tuning_epochs=15,
            max_trials=args.trials,
            save_path=args.output
        )
        
        print("\n" + "=" * 60)
        print("Training Completed!")
        print("=" * 60)
        print(f"Best Hyperparameters:")
        print(f"  Conv 1 Filters: {best_hps.get('conv_1_filter')}")
        print(f"  Conv 2 Filters: {best_hps.get('conv_2_filter')}")
        print(f"  Dense Units: {best_hps.get('dense_units')}")
        print(f"  Dropout Rate: {best_hps.get('dropout'):.2f}")
        print(f"  Learning Rate: {best_hps.get('learning_rate'):.0e}")
        
    else:
        print("Training model...")
        model, history = trainer.train_simple(
            epochs=args.epochs,
            save_path=args.output
        )
        
        print("\n" + "=" * 60)
        print("Training Completed!")
        print("=" * 60)
    
    # Show final metrics
    final_acc = history.history['accuracy'][-1]
    final_val_acc = history.history['val_accuracy'][-1]
    final_loss = history.history['loss'][-1]
    final_val_loss = history.history['val_loss'][-1]
    
    print(f"Final Training Accuracy: {final_acc:.2%}")
    print(f"Final Validation Accuracy: {final_val_acc:.2%}")
    print(f"Final Training Loss: {final_loss:.4f}")
    print(f"Final Validation Loss: {final_val_loss:.4f}")
    print(f"\nModel saved to: {args.output}")
    print("=" * 60)


if __name__ == "__main__":
    main()
