import tri
import lptri


children = (
	( 'tri', 'triangulaMonotono', 'Triangula Monotono' ),
	( 'lptri', 'lp', 'Triangula Lee e Preparata' ), 
)

__all__ = map (lambda a: a[0], children)
