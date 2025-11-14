{% if cookiecutter.project_type == 'rust-backed' -%}
//! {{cookiecutter.short_description}}
//!
//! This module provides Rust-backed high-performance implementations for {{cookiecutter.__package_name}}.

use pyo3::prelude::*;

/// Example function that adds two numbers
///
/// # Arguments
///
/// * `a` - First number
/// * `b` - Second number
///
/// # Returns
///
/// Sum of a and b
#[pyfunction]
fn add(a: i64, b: i64) -> PyResult<i64> {
    Ok(a + b)
}

/// {{cookiecutter.__package_name}} - {{cookiecutter.short_description}}
///
/// This module provides high-performance Rust implementations.
#[pymodule]
fn _{{cookiecutter.__package_name}}_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add, m)?)?;
    Ok(())
}
{%- endif %}
