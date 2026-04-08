"""
conftest.py — carregado automaticamente pelo pytest.
Garante que todos os models estão registrados no Base antes dos testes rodarem.
"""
# Estes imports precisam vir antes de qualquer uso de Base.metadata
import models.transaction  # noqa: F401
import models.user          # noqa: F401
